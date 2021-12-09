//4 bit in round robin mode

//4 request and 4 ground

module round_r (
    clk,
    rst_n,
    req,
    grant
   );

input rst_n;
input clk;
input [3:0] req;
output   [3:0] grant;

reg  [1:0] rotate_r;
reg  [3:0] shift_buf;
reg  [3:0] shift_grant;
reg  [3:0] grant_buf;



//----
always @ ( * ) begin
   case (rotate_r)
      2'b00: shift_buf[3:0] = req[3:0];
      2'b01: shift_buf[3:0] = {req[0], req[3:1]};
      2'b02: shift_buf[3:0] = {req[1:0], req[3:2] };
      2'b03: shift_buf[3:0] = {req[2:0], req[3]};
   endcase
end

always @ ( * ) begin
   shift_grant = 4'b0;
   if (shift_buf[0]) shift_grant[0] = 1'b1;
   else if (shift_buf[1]) shift_grant[1] = 1'b1;
   else if (shift_buf[2]) shift_grant[2] = 1'b1;
   else if (shift_buf[3]) shift_grant[3] = 1'b1;
end

//grant signal
always @ ( * ) begin
   case (rotate_r)
      2'b00: grant_buf = shift_grant;
      2'b01: grant_buf = {shift_grant[2:0], shift_grant[3]};
      2'b02: grant_buf = {shift_grant[1:0], shift_grant[3:2]};
      2'b03: grant_buf = {shift_grant[0], shift_grant[3:1]};
   endcase
end

always @ ( posedge clk or negedge rst_n ) begin
   if(!rst_n) grant[3:0] <= 4'b0;
   else grant[3:0] <= grant_buf[3:0] & ~grant[3:0];
end

always @ ( posedge clk or negedge rst_n ) begin
   begin
   if(!rst_n) round_r[1:0] <= 'd0;
   else
   case (1'b1)
      grant[0]: round_r[1:0] <= 2'b01;
      grant[1]: round_r[1:0] <= 2'b10;
      grant[2]: round_r[1:0] <= 2'b11;
      grant[3]: round_r[1:0] <= 2'b00;
   endcase
end

endmodule // round_r
